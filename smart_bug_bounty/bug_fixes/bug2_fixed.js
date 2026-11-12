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
console.log("Test 1 (Prototype Pollution Prevention):", !guestUser.isAdmin ? "PASS" : "FAIL");

const nestedTarget = {};
mergeConfig(nestedTarget, { server: { port: 8080 } });
console.log("Test 2 (Nested Merge):", nestedTarget.server && nestedTarget.server.port === 8080 ? "PASS" : "FAIL");

const safeTarget = { a: 1 };
mergeConfig(safeTarget, null);
console.log("Test 3 (Null Source):", safeTarget.a === 1 ? "PASS" : "FAIL");
