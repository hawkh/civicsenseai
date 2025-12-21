export async function createIssue(params: {
  imageBase64: string;
  description: string;
  latitude: number;
  longitude: number;
}) {
  if (
    typeof params.latitude !== "number" ||
    typeof params.longitude !== "number"
  ) {
    throw new Error("Invalid coordinates");
  }

  const payload = {
    image_url: params.imageBase64,
    description: params.description,
    location: {
      lat: params.latitude,
      lng: params.longitude,
    },
  };

  const res = await fetch(
    "https://backend-1005385950490.us-central1.run.app/api/v1/issues",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text);
  }

  return await res.json();
}
