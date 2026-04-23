import http from 'k6/http';
import { check, sleep } from 'k6';
import { randomName, randomPrice } from './helpers.js';

export const options = {
    stages: [
        { duration: '10s', target: 2 },   // Разогрев: 2 пользователя
        { duration: '20s', target: 5 },   // Пик: 5 пользователей
        { duration: '10s', target: 0 },   // Спад
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'],
        http_req_failed: ['rate<0.05'],
    },
};

const BASE_URL = 'http://localhost:8000';

export default function () {
    let getRes = http.get(`${BASE_URL}/items`);

    check(getRes, {
        'GET /items status is 200': (r) => r.status === 200,
        'GET returns array': (r) => Array.isArray(JSON.parse(r.body)),
    });

    sleep(1);

    const newItem = {
        name: randomName(),
        price: randomPrice()
    };

    let postRes = http.post(`${BASE_URL}/items`, JSON.stringify(newItem), {
        headers: { 'Content-Type': 'application/json' },
    });

    check(postRes, {
        'POST status is 201': (r) => r.status === 201,
        'POST returns item with id': (r) => JSON.parse(r.body).id !== undefined,
    });

    let createId = null;
    if(postRes.status === 201) {
        createId = JSON.parse(postRes.body).id;
    }

    sleep(1);

    if(createId) {
        let getByIdRes = http.get(`${BASE_URL}/items/${createId}`);

        check(getByIdRes, {
            'GET /items/:id status is 200': (r) => r.status === 200,
            'GET returns correct id': (r) => JSON.parse(r.body).id === createId,
        });
    }

    sleep(1);

    if(createId) {
        const updateItem = {
            name: `Updated ${randomName()}`,
            price: randomPrice()
        };

        let putRes = http.put(`${BASE_URL}/items/${createId}`, JSON.stringify(updateItem), {
            headers: { 'Content-Type': 'application/json' },
        });

        check(putRes, {
            'PUT status is 200': (r) => r.status === 200,
            'PUT updates name': (r) => JSON.parse(r.body).name === updateItem.name
        });
    }

    sleep(1);

    if(createId) {
        let delItem = http.del(`${BASE_URL}/items/${createId}`);

        check(delItem, {
            'DELETE status is 204': (r) => r.status === 204
        });
    }

    sleep(1);

    let statusRes = http.get(`${BASE_URL}/stats`);

    check(statusRes, {
        'GET /stats status is 200': (r) => r.status === 200,
    });

    sleep(1);
}