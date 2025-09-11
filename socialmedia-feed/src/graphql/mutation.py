mutation {
  tokenAuth(username: "alice", password: "secret") {
    token
  }
}
createPost(content: "Hello GraphQL world", mediaUrl: "https://...") {
    post {
      id
      content
      author {
        username
      }
}
}
toggleLike(postId: "1") {
    liked
    likesCount
  }
addComment(postId: "1", content: "Nice post!") {
    comment {
      id
      content
      author {
        username
      }
}
}
