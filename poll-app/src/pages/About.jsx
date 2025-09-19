function About() {
  return (
    <div className="max-w-3xl mx-auto py-10 px-6">
      <h2 className="text-3xl font-bold mb-4">About Polling App</h2>
      <p className="mb-4">
        Polling App is a simple application where users can create polls, vote,
        and view results instantly. It’s built with Django REST Framework (for
        backend) and React (for frontend).
      </p>
      <p className="mb-4">
        This project was developed by <strong>Bello Rasheed</strong> as part of
        a certification program. It demonstrates authentication, RESTful APIs,
        frontend integration, and deployment.
      </p>
      <h3 className="text-xl font-semibold mt-6 mb-2">FAQ</h3>
      <ul className="list-disc pl-6">
        <li> How do I create a poll? → Login and go to Polls page.</li>
        <li> Can I vote more than once? → No, one vote per user.</li>
        <li> Do I need an account? → Yes, login is required.</li>
      </ul>
    </div>
  );
}

export default About;
