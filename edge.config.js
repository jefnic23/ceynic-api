// edge.config.js

module.exports = {
  routes: [
    {
      path: "/public/*",
      origin: "https://bucketeer-dcd2d5ec-7312-40dc-a467-76b9f229f547.s3.amazonaws.com",
      cache: {
        ttl: 31536000, // 1 year
        bypassCookies: true
      },
      headers: {
        "Cache-Control": "public, max-age=31536000, immutable"
      }
    }
  ]
};
