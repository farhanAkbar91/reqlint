/** @type {import('next').NextConfig} */
const nextConfig = {
  outputFileTracing: false,
  async redirects() {
    return [
      {
        source: '/upload',
        destination: '/editor',
        permanent: false,
      },
      {
        source: '/signup',
        destination: '/register',
        permanent: false,
      },
      {
        source: '/audit',
        destination: '/editor',
        permanent: false,
      },
      {
        source: '/audit/hasilAudit',
        destination: '/history',
        permanent: false,
      },
    ];
  },
};

module.exports = nextConfig;
