import { apiClient } from "./client";

export const api = {
    generatePPT: (data) => apiClient.post("/generate/ppt", data),
    generatePodcast: (data) => apiClient.post("/generate/podcast", data),
    getJob: (jobId) => apiClient.get(`/job/${jobId}`),
    chat: (data) => apiClient.post("/chat", data)
};
