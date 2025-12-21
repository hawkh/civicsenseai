
import { CivicIssue, IssueStatus, Location } from "../types";

const API_BASE =
  "https://backend-1005385950490.us-central1.run.app";

export async function createIssue(params: {
  imageBase64: string;
  description: string;
  location: Location;
}): Promise<CivicIssue> {
  const res = await fetch(`${API_BASE}/api/v1/issues`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      image_url: params.imageBase64, // TEMP (base64)
      description: params.description,
      location: {
        lat: params.location.latitude,
        lng: params.location.longitude,
      },
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || "Issue creation failed");
  }

  const data = await res.json();

  return {
    id: data.issue_id,
    description: params.description,
    image_url: params.imageBase64,
    location: params.location,
    status: data.status as IssueStatus,
  };
}
