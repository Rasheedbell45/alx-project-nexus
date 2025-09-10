import axios from "axios";

const API_URL = "https://remotive.io/api/remote-jobs";

export const fetchJobs = async () => {
  const res = await axios.get(API_URL);
  return res.data.jobs;
};
