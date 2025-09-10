import styled from "styled-components";

export const Card = styled.div`
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  transition: transform 0.2s;
  cursor: pointer;

  &:hover {
    transform: scale(1.05);
  }

  img {
    width: 100%;
  }

  h3 {
    margin: 0.5rem;
    font-size: 1rem;
  }
`;
