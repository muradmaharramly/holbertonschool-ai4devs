function mergeConfig(target, source) {
    if (!source || typeof source !== "object") {
        return target;
    }
    for (const key of Object.keys(source)) {
        if (key === "__proto__" || key === "constructor" || key === "prototype") {
            continue;
        }
        if (typeof source[key] === "object" && source[key] !== null && !Array.isArray(source[key])) {
            if (!target[key] || typeof target[key] !== "object") {
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
