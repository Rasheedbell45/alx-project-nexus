# 🎬 Movie Catalog (Next.js + TypeScript)

## 🚀 Features
- Dynamic movie list with **TMDB API**
- **Detailed movie pages** with dynamic routing
- Save and manage **favorite movies**
- Styled with **Styled Components**
- 
# Movie Backend

ENV:
- TMDB_API_KEY=your_tmdb_api_key
- POSTGRES_*
- REDIS_URL

Run (local):
- docker-compose up --build
- create superuser: docker exec -it <web> python manage.py createsuperuser
- Visit: http://localhost:8000/api/docs/ for Swagger UI
