
/**
 * Compresses a base64 image string by resizing it to a maximum dimension
 * and reducing quality.
 *
 * @param base64Str The original base64 image string
 * @param maxWidth Maximum width (default 800px)
 * @param maxHeight Maximum height (default 800px)
 * @param quality Image quality 0-1 (default 0.7)
 * @returns Promise resolving to the compressed base64 string
 */
export const compressImage = (
  base64Str: string,
  maxWidth = 800,
  maxHeight = 800,
  quality = 0.7
): Promise<string> => {
  return new Promise((resolve) => {
    const img = new Image();
    img.src = base64Str;
    img.onload = () => {
      const canvas = document.createElement('canvas');
      let width = img.width;
      let height = img.height;

      // Calculate new dimensions
      if (width > height) {
        if (width > maxWidth) {
          height *= maxWidth / width;
          width = maxWidth;
        }
      } else {
        if (height > maxHeight) {
          width *= maxHeight / height;
          height = maxHeight;
        }
      }

      canvas.width = width;
      canvas.height = height;

      const ctx = canvas.getContext('2d');
      if (!ctx) {
        resolve(base64Str); // Fallback if context fails
        return;
      }

      ctx.drawImage(img, 0, 0, width, height);
      resolve(canvas.toDataURL('image/jpeg', quality));
    };
    img.onerror = () => {
      resolve(base64Str); // Fallback on error
    };
  });
};
