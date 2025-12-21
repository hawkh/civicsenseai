export async function createIssue(params: {
  imageBase64?: string;
  description: string;
  latitude: number;
  longitude: number;
}) {
  const { imageBase64, description, latitude, longitude } = params;

  if (
    typeof latitude !== "number" ||
    typeof longitude !== "number" ||
    Number.isNaN(latitude) ||
    Number.isNaN(longitude)
  ) {
    throw new Error("Invalid coordinates");
  }
const payload = {
  image_url: imageBase64 ?? null,
  description,
  location: {
    lat: Number(latitude),
    lng: Number(longitude),
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
    throw new Error(text || "Issue creation failed");
  }

  return await res.json();
}
