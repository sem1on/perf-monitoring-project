// Генерация случайного имени
export function randomName() {
    const ajectives = ['Gaming', 'Office', 'Ultra', 'Pro', 'Basic', 'Premium'];
    const nouns = ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headset', 'Tablet'];

    const adj = ajectives[Math.floor(Math.random() * ajectives.length)];
    const noum = nouns[Math.floor(Math.random() * nouns.length)];

    return `${adj} ${noum}`
}

// Генерация случайной цены (от 100 до 1000)
export function randomPrice() {
    return Number((Math.random() * 900 + 100).toFixed(2));
}

// Проверка ответа с логированием
export function checkResponce(responce, expectedStatus, operation) {
    const success = responce.status === expectedStatus;

    if (!success) {
        console.error(`❌ ${operation} failed: status ${response.status}`);
    } else {
        console.log(`✅ ${operation} successful (${response.status})`)
    }

    return success;
}