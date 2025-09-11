query {
  posts(first: 10, contains: "frontend") {
    edges {
      node {
        id
        content
        author {
          username
        }
        likesCount
        commentsCount
      }
    }
  }
}
