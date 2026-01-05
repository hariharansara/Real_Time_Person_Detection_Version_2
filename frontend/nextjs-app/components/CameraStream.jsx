"use client";
import { useEffect, useRef, useState } from "react";
import { identifyFrame } from "../services/identify";

export default function CameraStream() {
  const videoRef = useRef(null);
  const [result, setResult] = useState("Waiting for detection...");

  useEffect(() => {
    async function startCamera() {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true });
      videoRef.current.srcObject = stream;
    }
    startCamera();
  }, []);

  useEffect(() => {
    const interval = setInterval(async () => {
      const video = videoRef.current;
      if (!video) return;

      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      canvas.toBlob(async (blob) => {
        if (!blob) return;
        const data = await identifyFrame(blob);
        setResult(`${data.person} | ${data.status}`);
      }, "image/jpeg");
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <video
        ref={videoRef}
        autoPlay
        playsInline
        width="500"
        style={{ border: "2px solid black", borderRadius: 8, marginTop: 20 }}
      />
      <h2 style={{ marginTop: 20 }}>{result}</h2>
    </div>
  );
}
