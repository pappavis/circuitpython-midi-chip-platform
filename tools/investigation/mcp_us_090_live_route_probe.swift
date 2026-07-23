/*
 Bestand: mcp_us_090_live_route_probe.swift
 Versienommer: 0.1.0
 Doel: Temporary native CoreMIDI live route probe for MCP-US-090.
 Sprint: P0 Investigation
 Epic: MCP-EPIC-USB-MIDI
 User-Story: MCP-US-090 Live CoreMIDI Endpoint Attribution and Controlled MIDI Route Proof
 Actienr: MCP-US-090-LIVE-ROUTE-PROBE-001
 ChatID: CHATOD-20260714-MCP-CP-MVP-001 / MCP-US-090

 Investigation-only helper. Do not ship as product code.
 */

import CoreMIDI
import Foundation

@main
struct McpUs090LiveRouteProbe {
    private let targetUniqueID: MIDIUniqueID = 2064399636
    private let clientName = "MCP-US-090 Live Route Probe"
    private let outputPortName = "MCP-US-090 Output Port"

    static func main() {
        McpUs090LiveRouteProbe().run()
    }

    private func run() {
        log("MCP_US_090_HELPER_STATUS=START")
        log("RTMIDI_USED=false")
        log("TARGET_DESTINATION_UNIQUEID=\(targetUniqueID)")

        let matches = destinations(matching: targetUniqueID)
        log("DESTINATION_MATCH_COUNT=\(matches.count)")

        guard matches.count == 1, let destination = matches.first else {
            log("LIVE_DESTINATION_IDENTIFICATION=FAIL")
            log("reason=target_unique_id_missing_or_not_unique")
            exit(2)
        }

        logDestination(destination)

        var client = MIDIClientRef()
        let clientStatus = MIDIClientCreate(clientName as CFString, nil, nil, &client)
        log("COREMIDI_CALL=MIDIClientCreate;status=\(clientStatus)")
        guard clientStatus == noErr else {
            log("HOST_SEND_STATUS=FAIL;reason=MIDIClientCreate_status_\(clientStatus)")
            exit(3)
        }

        var outputPort = MIDIPortRef()
        let portStatus = MIDIOutputPortCreate(client, outputPortName as CFString, &outputPort)
        log("COREMIDI_CALL=MIDIOutputPortCreate;status=\(portStatus)")
        guard portStatus == noErr else {
            MIDIClientDispose(client)
            log("HOST_SEND_STATUS=FAIL;reason=MIDIOutputPortCreate_status_\(portStatus)")
            exit(4)
        }

        log("HOST_PATTERN_BEGIN;monotonic_ns=\(DispatchTime.now().uptimeNanoseconds);wall_clock=\(isoTimestamp())")
        let events = controlledPattern()
        var allSucceeded = true
        for event in events {
            sleepNanoseconds(event.delayBeforeNanoseconds)
            let sendStatus = send(event: event, to: destination.ref, through: outputPort)
            allSucceeded = allSucceeded && sendStatus == noErr
        }
        log("HOST_PATTERN_END;monotonic_ns=\(DispatchTime.now().uptimeNanoseconds);wall_clock=\(isoTimestamp())")

        MIDIPortDispose(outputPort)
        MIDIClientDispose(client)
        log("COREMIDI_RESOURCES_DISPOSED=true")

        if allSucceeded {
            log("HOST_SEND_STATUS=PASS")
            exit(0)
        }

        log("HOST_SEND_STATUS=FAIL;reason=one_or_more_MIDISend_calls_failed")
        exit(5)
    }

    private func destinations(matching uniqueID: MIDIUniqueID) -> [DestinationInfo] {
        let count = MIDIGetNumberOfDestinations()
        log("COREMIDI_DESTINATION_COUNT=\(count)")
        var matches = [DestinationInfo]()

        for index in 0..<count {
            let endpoint = MIDIGetDestination(index)
            let info = DestinationInfo(
                ref: endpoint,
                index: index,
                name: stringProperty(endpoint, key: kMIDIPropertyName),
                displayName: stringProperty(endpoint, key: kMIDIPropertyDisplayName),
                manufacturer: stringProperty(endpoint, key: kMIDIPropertyManufacturer),
                driver: stringProperty(endpoint, key: kMIDIPropertyDriverOwner),
                model: stringProperty(endpoint, key: kMIDIPropertyModel),
                uniqueID: integerProperty(endpoint, key: kMIDIPropertyUniqueID)
            )
            log("DESTINATION_CANDIDATE;index=\(info.index);name=\(info.name);displayName=\(info.displayName);manufacturer=\(info.manufacturer);driver=\(info.driver);model=\(info.model);uniqueID=\(info.uniqueIDText)")
            if info.uniqueID == uniqueID {
                matches.append(info)
            }
        }
        return matches
    }

    private func logDestination(_ destination: DestinationInfo) {
        log("LIVE_DESTINATION_IDENTIFICATION=PASS")
        log("LIVE_DESTINATION;index=\(destination.index);name=\(destination.name);displayName=\(destination.displayName);manufacturer=\(destination.manufacturer);driver=\(destination.driver);model=\(destination.model);uniqueID=\(destination.uniqueIDText)")
    }

    private func controlledPattern() -> [MidiEvent] {
        [
            MidiEvent(delayBeforeNanoseconds: 0, eventType: "control_change", channel: 16, data1: 119, data2: 23),
            MidiEvent(delayBeforeNanoseconds: 300_000_000, eventType: "note_on", channel: 16, data1: 61, data2: 37),
            MidiEvent(delayBeforeNanoseconds: 650_000_000, eventType: "note_off", channel: 16, data1: 61, data2: 0),
            MidiEvent(delayBeforeNanoseconds: 350_000_000, eventType: "note_on", channel: 16, data1: 66, data2: 79),
            MidiEvent(delayBeforeNanoseconds: 650_000_000, eventType: "note_off", channel: 16, data1: 66, data2: 0),
            MidiEvent(delayBeforeNanoseconds: 350_000_000, eventType: "note_on", channel: 16, data1: 70, data2: 113),
            MidiEvent(delayBeforeNanoseconds: 650_000_000, eventType: "note_off", channel: 16, data1: 70, data2: 0),
        ]
    }

    private func send(event: MidiEvent, to destination: MIDIEndpointRef, through outputPort: MIDIPortRef) -> OSStatus {
        let bytes = event.rawBytes()
        var packetList = MIDIPacketList()
        let packet = MIDIPacketListInit(&packetList)
        _ = MIDIPacketListAdd(&packetList, 1024, packet, 0, bytes.count, bytes)

        let sendStatus = MIDISend(outputPort, destination, &packetList)
        log("HOST_EVENT;monotonic_ns=\(DispatchTime.now().uptimeNanoseconds);wall_clock=\(isoTimestamp());destination_uniqueID=\(targetUniqueID);client=\(clientName);output_port=\(outputPortName);eventtype=\(event.eventType);channel=\(event.channel);data1=\(event.data1);data2=\(event.data2);raw_bytes=\(bytes);coremidi_status=\(sendStatus)")
        return sendStatus
    }

    private func stringProperty(_ object: MIDIObjectRef, key: CFString) -> String {
        var unmanaged: Unmanaged<CFString>?
        let status = MIDIObjectGetStringProperty(object, key, &unmanaged)
        guard status == noErr, let value = unmanaged?.takeRetainedValue() else {
            return "UNKNOWN(status=\(status))"
        }
        return value as String
    }

    private func integerProperty(_ object: MIDIObjectRef, key: CFString) -> MIDIUniqueID? {
        var value: Int32 = 0
        let status = MIDIObjectGetIntegerProperty(object, key, &value)
        guard status == noErr else {
            return nil
        }
        return MIDIUniqueID(value)
    }

    private func sleepNanoseconds(_ nanoseconds: UInt64) {
        guard nanoseconds > 0 else {
            return
        }
        Thread.sleep(forTimeInterval: Double(nanoseconds) / 1_000_000_000.0)
    }

    private func isoTimestamp() -> String {
        ISO8601DateFormatter().string(from: Date())
    }

    private func log(_ message: String) {
        print(message)
        fflush(stdout)
    }
}

private struct DestinationInfo {
    let ref: MIDIEndpointRef
    let index: Int
    let name: String
    let displayName: String
    let manufacturer: String
    let driver: String
    let model: String
    let uniqueID: MIDIUniqueID?

    var uniqueIDText: String {
        guard let uniqueID else {
            return "UNKNOWN"
        }
        return String(uniqueID)
    }
}

private struct MidiEvent {
    let delayBeforeNanoseconds: UInt64
    let eventType: String
    let channel: UInt8
    let data1: UInt8
    let data2: UInt8

    func rawBytes() -> [UInt8] {
        let statusBase: UInt8 = eventType == "note_off" ? 0x80 : eventType == "note_on" ? 0x90 : 0xB0
        return [statusBase + (channel - 1), data1, data2]
    }
}
