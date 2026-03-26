import http from 'k6/http';
import { sleep } from 'k6';

const LAMBDA_URL = 'https://r4kv3dlxvaozigftwaupiimvhu0kmcsk.lambda-url.us-east-1.on.aws/';

export const options = {
  scenarios: {
    concurrency_test: {
      executor: 'ramping-vus',
      startVUs: 1,
      stages: [
        { duration: '60s', target: 1   },
        { duration: '60s', target: 10  },
        { duration: '60s', target: 50  },
        { duration: '60s', target: 100 },
        { duration: '60s', target: 200 },
        { duration: '30s', target: 0   },
      ],
    },
  },
};

export default function () {
  http.get(LAMBDA_URL);
}