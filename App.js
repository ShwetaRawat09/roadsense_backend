import React, { useState, useEffect } from "react";
import { StyleSheet, Text, View, TouchableOpacity, ScrollView, ActivityIndicator, Platform } from "react-native";
import { ShieldCheck, AlertTriangle, Radio } from "lucide-react-native";
import { Accelerometer } from "expo-sensors";
import MapComponent from "./MapComponent";

export default function App() {
  const [roads, setRoads] = useState([]);
  const [isRecording, setIsRecording] = useState(false);
  const [lastJerk, setLastJerk] = useState(0);

  // 1. Telemetry Recording Logic
  useEffect(() => {
    let subscription;
    if (isRecording) {
      Accelerometer.setUpdateInterval(100); // 10 samples per second
      subscription = Accelerometer.addListener(data => {
        const totalForce = Math.abs(data.x) + Math.abs(data.y) + Math.abs(data.z);
        if (totalForce > 2.5) { // Threshold for a "Bump"
          setLastJerk(totalForce.toFixed(2));
          sendBumpToBackend(totalForce);
        }
      });
    }
    return () => subscription && subscription.remove();
  }, [isRecording]);

  const sendBumpToBackend = async (jerkValue) => {
    try {
      await fetch("http://127.0.0.1:8000/record-bump", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          max_jerk: jerkValue,
          lat: 13.0827, // Default Chennai center
          lon: 80.2707
        })
      });
    } catch (e) {
      console.log("Error uploading bump data");
    }
  };

  const fetchData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/top-10-roads?ward_id=1");
      const data = await response.json();
      setRoads(data.priority_segments);
    } catch (e) { alert("Backend connection failed!"); }
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>RoadSense Pro</Text>
        <Text style={styles.subtitle}>Real-time Hardware Telemetry</Text>
      </View>

      <View style={styles.mapContainer}>
        <MapComponent roads={roads} />
      </View>

      <ScrollView style={styles.statsContainer}>
        {/* Record Button */}
        <TouchableOpacity 
          style={[styles.recordButton, isRecording && { backgroundColor: "#ff7675" }]} 
          onPress={() => setIsRecording(!isRecording)}
        >
          <Radio color="white" size={20} style={{marginRight: 10}} />
          <Text style={styles.buttonText}>{isRecording ? `Recording... (${lastJerk})` : "Start Live Capture"}</Text>
        </TouchableOpacity>

        <TouchableOpacity style={styles.fetchButton} onPress={fetchData}>
          <Text style={styles.buttonText}>Refresh Ward Analysis</Text>
        </TouchableOpacity>

        {roads.map((road, index) => (
          <View key={index} style={styles.card}>
            <View style={styles.cardIcon}>
              {road.health_score < 50 ? <AlertTriangle color="#e74c3c" size={24} /> : <ShieldCheck color="#2ecc71" size={24} />}
            </View>
            <View style={styles.cardInfo}>
              <Text style={styles.roadId}>{road.segment_id}</Text>
              <Text style={styles.roadMeta}>Health Score: {road.health_score}%</Text>
            </View>
          </View>
        ))}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#F5F7FA" },
  header: { paddingTop: 60, paddingBottom: 20, paddingHorizontal: 20, backgroundColor: "white" },
  title: { fontSize: 24, fontWeight: "bold", color: "#2D3436" },
  subtitle: { fontSize: 14, color: "#636E72" },
  mapContainer: { height: 250, width: "100%" },
  statsContainer: { flex: 1, padding: 20 },
  recordButton: { backgroundColor: "#d63031", padding: 16, borderRadius: 12, flexDirection: "row", justifyContent: "center", alignItems: "center", marginBottom: 10 },
  fetchButton: { backgroundColor: "#0984E3", padding: 16, borderRadius: 12, alignItems: "center", marginBottom: 20 },
  buttonText: { color: "white", fontWeight: "bold", fontSize: 16 },
  card: { backgroundColor: "white", padding: 15, borderRadius: 12, flexDirection: "row", alignItems: "center", marginBottom: 10, elevation: 2 },
  cardIcon: { marginRight: 15 },
  cardInfo: { flex: 1 },
  roadId: { fontWeight: "700" },
  roadMeta: { fontSize: 13, color: "#636E72" }
});
