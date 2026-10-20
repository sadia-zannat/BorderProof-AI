FROM node:22-alpine AS builder
WORKDIR /workspace/apps/web
COPY apps/web/package*.json ./
RUN npm ci --no-audit --no-fund
COPY apps/web ./
ARG NEXT_PUBLIC_API_BASE_URL=
ENV NEXT_PUBLIC_API_BASE_URL=${NEXT_PUBLIC_API_BASE_URL}
RUN npm run build
FROM node:22-alpine
WORKDIR /workspace/apps/web
COPY --from=builder /workspace/apps/web ./
ENV NODE_ENV=production
EXPOSE 3000
CMD ["npm","run","start"]
