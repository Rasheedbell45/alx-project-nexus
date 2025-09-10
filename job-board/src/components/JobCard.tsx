import React from "react";
import styled from "styled-components";

const Card = styled.div`
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 1rem;
  background: #fff;
  transition: box-shadow 0.2s ease;
  cursor: pointer;

  &:hover {
    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
  }

  h3 {
    margin: 0;
  }

  @media (max-width: 600px) {
    padding: 0.8rem;
    h3 {
      font-size: 1rem;
    }
  }
`;

export default function JobCard({ job }: { job: any }) {
  return (
    <Card>
      <h3>{job.title}</h3>
      <p>🏢 {job.company_name}</p>
      <p>📂 {job.category}</p>
      <p>🌍 {job.candidate_required_location}</p>
      <a href={job.url} target="_blank" rel="noopener noreferrer">
        View Details
      </a>
    </Card>
  );
}
