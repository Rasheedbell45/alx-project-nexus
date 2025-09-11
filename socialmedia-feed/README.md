# Social Media Feed Project

A React + GraphQL project simulating a real-world **social media feed**.

## 🚀 Features
- Dynamic feed from GraphQL API
- Like, Comment, Share interactions
- Pagination + Infinite Scroll
- Responsive UI with animations

## 🛠️ Tech Stack
- React + TypeScript
- Apollo GraphQL
- Tailwind CSS
- Framer Motion

## ▶️ Getting Started
```bash
git clone <repo>
cd social-feed
npm install
npm start

# Social Backend (GraphQL)

## GraphQL Playground
Visit: /graphql/ (GraphiQL)

## Authentication
Obtain JWT:
mutation {
  tokenAuth(username: "user", password: "pass") { token }
}

Include token in Authorization header for protected mutations:
Authorization: Bearer <token>

## Queries
- posts(first: 10)
- post(id: ID)

## Mutations
- createPost(content, mediaUrl)
- addComment(postId, content)
- toggleLike(postId)
- sharePost(postId)
