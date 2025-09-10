import { createSlice, PayloadAction } from "@reduxjs/toolkit";

interface Option {
  id: number;
  text: string;
  votes: number;
}

interface PollState {
  question: string;
  options: Option[];
}

const initialState: PollState = {
  question: "What’s your favorite frontend framework?",
  options: [
    { id: 1, text: "React", votes: 0 },
    { id: 2, text: "Vue", votes: 0 },
    { id: 3, text: "Angular", votes: 0 },
  ],
};

const pollSlice = createSlice({
  name: "poll",
  initialState,
  reducers: {
    vote: (state, action: PayloadAction<number>) => {
      const option = state.options.find((opt) => opt.id === action.payload);
      if (option) option.votes += 1;
    },
    createPoll: (state, action: PayloadAction<{ question: string; options: string[] }>) => {
      state.question = action.payload.question;
      state.options = action.payload.options.map((text, idx) => ({
        id: idx + 1,
        text,
        votes: 0,
      }));
    },
  },
});

export const { vote, createPoll } = pollSlice.actions;
export default pollSlice.reducer;
