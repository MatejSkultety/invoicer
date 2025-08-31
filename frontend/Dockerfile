# Frontend Dockerfile (Placeholder for Vue.js app)
# This serves a simple HTML page until Vue.js is implemented

FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy the source files
COPY frontend/src/ ./src/

# Install a simple HTTP server
RUN npm install -g http-server

# Create a startup script
RUN echo '#!/bin/sh' > start.sh && \
    echo 'echo "🚀 Frontend service starting..."' >> start.sh && \
    echo 'echo "📁 Serving files from /app/src"' >> start.sh && \
    echo 'echo "🌐 Server running on http://0.0.0.0:3000"' >> start.sh && \
    echo 'echo "⚡ Vue.js application will be implemented here"' >> start.sh && \
    echo 'echo ""' >> start.sh && \
    echo 'cd src && http-server -p 3000 -a 0.0.0.0 --cors' >> start.sh && \
    chmod +x start.sh

# Expose the port that nginx expects
EXPOSE 3000

# Start the HTTP server
CMD ["./start.sh"]