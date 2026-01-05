"use client";
import CameraStream from "../components/CameraStream";

export default function Home() {
  return (
    <div style={{ textAlign: "center", paddingTop: 40 }}>
      <h1>Live Person Identification AI</h1>
      <CameraStream />
    </div>
  );
}
