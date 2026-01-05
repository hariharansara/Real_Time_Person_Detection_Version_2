export async function identifyFrame(frameBlob) {
  const formData = new FormData();
  formData.append("file", frameBlob);

  try {
    const response = await fetch("http://127.0.0.1:8000/predict", {
      method: "POST",
      body: formData,
    });

    return await response.json();
  } catch (err) {
    console.log("Fetch Error:", err);
    return { person: "No Response", status: "error" };
  }
}
