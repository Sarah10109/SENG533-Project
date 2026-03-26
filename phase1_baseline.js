import http from 'k6/http';

const LAMBDA_URL = 'https://r4kv3dlxvaozigftwaupiimvhu0kmcsk.lambda-url.us-east-1.on.aws/';

export const options = {
  vus: 1,
  iterations: 1,
};

export default function () {
  const res = http.get(LAMBDA_URL);
  console.log(`Status: ${res.status}, Duration: ${res.timings.duration}ms`);
}