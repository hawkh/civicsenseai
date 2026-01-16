import React, { useState, useRef, useEffect } from "react";
import { CivicIssue, Location } from "../types";
import { createIssue } from "../api/issues";

import {
  Camera,
  MapPin,
  X,
  ArrowRight,
  Loader2,
} from "lucide-react";

interface ReportScreenProps {
  onCancel: () => void;
  onSubmit: (issue: CivicIssue) => void;
}

const ReportScreen: React.FC<ReportScreenProps> = ({
  onCancel,
  onSubmit,
}) => {
  const [image, setImage] = useState<string | null>(null);
  const [description, setDescription] = useState("");
  const [location, setLocation] = useState<Location | null>(null);
  const [addressInput, setAddressInput] = useState("");
  const [isManual, setIsManual] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLocating, setIsLocating] = useState(false);
  const [locationError, setLocationError] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    requestLocation();
  }, []);

  // -------------------------
  // Location
  // -------------------------
  const requestLocation = () => {
    setIsLocating(true);
    setLocationError(null);
    setIsManual(false);

    if (!navigator.geolocation) {
      setLocationError("Geolocation not supported");
      setIsLocating(false);
      setIsManual(true);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (pos) => {
        setLocation({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
        });
        setIsLocating(false);
      },
      () => {
        setLocationError("GPS unavailable");
        setIsLocating(false);
        setIsManual(true);
      },
      { enableHighAccuracy: true, timeout: 10000 }
    );
  };

  // -------------------------
  // Image
  // -------------------------
  const handleFileChange = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onloadend = () => {
      setImage(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  // -------------------------
  // Submit (API aligned)
  // -------------------------
  const handleSubmit = async () => {
    if (!image || (!location && !addressInput)) return;

    setIsSubmitting(true);

    try {
      // Flatten location for API
      const finalLocation = location ?? { latitude: 0, longitude: 0 };

      const apiResult = await createIssue({
        imageBase64: image,
        description: description || "No description provided",
        latitude: finalLocation.latitude,
        longitude: finalLocation.longitude,
      });

      // 🔑 Backend is source of truth
      const issue: CivicIssue = {
        id: apiResult.id,              // ← issue_id
        status: apiResult.status,      // ← submitted
        description,
        image_url: image,
        location: location!,
      };

      onSubmit(issue);
    } catch (err) {
      console.error(err);
      setIsSubmitting(false);
    }
  };

  // -------------------------
  // UI
  // -------------------------
  return (
    <div className="h-full flex flex-col bg-white overflow-hidden">
      <header className="px-4 py-3 flex justify-between items-center border-b">
        <button onClick={onCancel}>
          <X />
        </button>
        <span className="text-xs font-bold uppercase">
          Report Issue
        </span>
        <div />
      </header>

      <div className="flex-1 p-4 space-y-4 overflow-y-auto">
        {/* Image */}
        {image ? (
          <div className="relative">
            <img
              src={image}
              className="rounded-xl"
              alt="evidence"
            />
            <button
              onClick={() => setImage(null)}
              className="absolute top-2 right-2"
            >
              <X />
            </button>
          </div>
        ) : (
          <button
            onClick={() => fileInputRef.current?.click()}
            className="border-dashed border p-6 rounded-xl w-full"
          >
            <Camera />
            <p>Upload Photo</p>
          </button>
        )}

        <input
          ref={fileInputRef}
          type="file"
          accept="image/*"
          hidden
          onChange={handleFileChange}
        />

        {/* Location */}
        {!isManual ? (
          <div className="flex items-center gap-2">
            <MapPin />
            {isLocating ? (
              <Loader2 className="animate-spin" />
            ) : location ? (
              <span>
                {location.latitude.toFixed(4)},{" "}
                {location.longitude.toFixed(4)}
              </span>
            ) : (
              <span className="text-red-500">
                {locationError}
              </span>
            )}
          </div>
        ) : (
          <input
            value={addressInput}
            onChange={(e) => setAddressInput(e.target.value)}
            placeholder="Enter address"
            className="border p-2 rounded w-full"
          />
        )}

        <button
          onClick={() => setIsManual(!isManual)}
          className="text-xs underline"
        >
          {isManual ? "Use GPS" : "Enter manually"}
        </button>

        {/* Description */}
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe the issue"
          className="border p-3 rounded w-full"
        />
      </div>

      <footer className="p-4 border-t">
        <button
          onClick={handleSubmit}
          disabled={isSubmitting}
          className="bg-indigo-600 text-white w-full py-3 rounded-xl flex items-center justify-center gap-2"
        >
          {isSubmitting ? (
            <>
              <Loader2 className="animate-spin" />
              Submitting
            </>
          ) : (
            <>
              Submit
              <ArrowRight />
            </>
          )}
        </button>
      </footer>
    </div>
  );
};

export default ReportScreen;
