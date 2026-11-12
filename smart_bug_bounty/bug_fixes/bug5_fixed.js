async function fetchUserMetrics(userIds, fetchMock) {
    if (!Array.isArray(userIds) || userIds.length === 0) {
        return [];
    }
    return Promise.all(userIds.map(id => fetchMock(id)));
}

const mockApi = (id) => new Promise(resolve => setTimeout(() => resolve({ id, score: id * 10 }), 10));

async function runTests() {
    const t1 = await fetchUserMetrics([1, 2, 3], mockApi);
    console.log("Test 1 (Multiple IDs):", t1.length === 3 && t1[2].score === 30 ? "PASS" : "FAIL");

    const t2 = await fetchUserMetrics([42], mockApi);
    console.log("Test 2 (Single ID):", t2.length === 1 && t2[0].id === 42 ? "PASS" : "FAIL");

    const t3 = await fetchUserMetrics([], mockApi);
    console.log("Test 3 (Empty Array):", Array.isArray(t3) && t3.length === 0 ? "PASS" : "FAIL");
}

runTests();
