function mergeConfig(target, source) {
    for (const key of Object.keys(source)) {
        if (typeof source[key] === "object" && source[key] !== null) {
            if (!target[key]) {
                target[key] = {};
            }
            mergeConfig(target[key], source[key]);
        } else {
            target[key] = source[key];
        }
    }
    return target;
}

const baseConfig = { env: "production", retries: 3 };
const userPayload = JSON.parse('{"__proto__": {"isAdmin": true}}');
mergeConfig(baseConfig, userPayload);

const guestUser = {};
console.log("Is guest admin:", Boolean(guestUser.isAdmin));
