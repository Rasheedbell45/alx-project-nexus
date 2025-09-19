import axios from "axios";

const API = axios.create({ baseURL: "http://127.0.0.1:8000/api" });

API.interceptors.request.use((req) => {
  if (localStorage.getItem("token")) {
    req.headers.Authorization = `Bearer ${localStorage.getItem("token")}`;
  }
  return req;
});

export const login = (data) => API.post("/users/login/", data);
export const getPolls = () => API.get("/polls/");
export const createPoll = (data) => API.post("/polls/", data);
export const vote = (data) => API.post("/polls/vote/", data);
export const getResults = (id) => API.get(`/polls/${id}/results/`);
