import axios from "axios";

const API = axios.create({ baseURL: "http://127.0.0.1:8000/api" });

API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

export const login = (data) => API.post("/users/login/", data);
export const register = (data) => API.post("/users/register/", data);
export const sendPasswordResetEmail = (data) => API.post("/users/forgot_password/", data);

export const getPolls = () => API.get("/polls/");
export const createPoll = (data) => API.post("/polls/", data);
export const votePoll = (pollId, optionId) =>
  API.post(`/polls/${pollId}/vote/`, { option_id: optionId });
export const getResults = (pollId) => API.get(`/polls/${pollId}/results/`);
