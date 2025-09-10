import React, { useEffect, useState } from "react";
import { fetchJobs } from "../api/jobs";
import JobCard from "./JobCard";

interface Job {
  id: number;
  title: string;
  company_name: string;
  category: string;
  candidate_required_location: string;
  url: string;
}

export default function JobList() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [category, setCategory] = useState("");
  const [location, setLocation] = useState("");

  useEffect(() => {
    fetchJobs().then(setJobs);
  }, []);

  const filteredJobs = jobs.filter((job) =>
    (category ? job.category.includes(category) : true) &&
    (location ? job.candidate_required_location.includes(location) : true)
  );

  return (
    <div>
      <h1>💼 Job Board</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input
          placeholder="Filter by category..."
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />
        <input
          placeholder="Filter by location..."
          value={location}
          onChange={(e) => setLocation(e.target.value)}
        />
      </div>

      <div style={{ display: "grid", gap: "1rem" }}>
        {filteredJobs.map((job) => (
          <JobCard key={job.id} job={job} />
        ))}
      </div>
    </div>
  );
}
