/**
 * Offer data as a file download from the browser
 * @param {string} data - data to download
 * @param {string} contentType - MIME type
 * @param {string} fileName - name of downloaded file
 */
export function downloadFile(data, contentType, fileName) {
    const blob = new Blob([data], {type: contentType})
    const url = window.URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = fileName || "download";
    anchor.click();
    window.URL.revokeObjectURL(url);
}