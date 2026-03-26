import http from 'k6/http';

const LAMBDA_URL = 'https://r4kv3dlxvaozigftwaupiimvhu0kmcsk.lambda-url.us-east-1.on.aws/';

export const options = {
  scenarios: {
    throughput_test: {
      executor: 'constant-arrival-rate',
      duration: '60s',
      rate: 100,           // change per round
      timeUnit: '1s',
      preAllocatedVUs: 50,
      maxVUs: 300,
    },
  },
};

export default function () {
  http.get(LAMBDA_URL);
}