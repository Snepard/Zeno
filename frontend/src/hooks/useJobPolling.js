import { useState, useEffect } from "react";
import { api } from "../api/endpoints";

export const useJobPolling = (jobId) => {
    const [jobData, setJobData] = useState(null);
    const [status, setStatus] = useState("queued");
    const [progress, setProgress] = useState(0);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!jobId) return;

        let interval;

        const pollJob = async () => {
            try {
                const res = await api.getJob(jobId);
                const data = res.data;
                
                setJobData(data);
                setStatus(data.status);
                setProgress(data.progress || 0);

                if (data.status === "completed" || data.status === "failed") {
                    clearInterval(interval);
                    if (data.status === "failed") {
                         setError(data.error || "Execution failed entirely resolving boundaries.");
                    }
                }
            } catch (err) {
                console.error("Critical polling sequence fault:", err);
            }
        };

        if (status !== "completed" && status !== "failed") {
             pollJob();
             interval = setInterval(pollJob, 2000);
        }

        return () => clearInterval(interval);
    }, [jobId, status]);

    return { jobData, status, progress, error };
};
