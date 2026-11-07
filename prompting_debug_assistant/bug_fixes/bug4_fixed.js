function aggregateProductMetrics(products) {
    const validPrices = products
        .map(p => parseFloat(p.price))
        .filter(price => !isNaN(price));

    const sortedPrices = validPrices.sort((a, b) => a - b);
    
    let totalRevenue = 0;
    for (let i = 0; i < sortedPrices.length; i++) {
        totalRevenue += sortedPrices[i];
    }

    const median = sortedPrices[Math.floor(sortedPrices.length / 2)];

    return {
        sortedPrices: sortedPrices,
        totalRevenue: Number(totalRevenue.toFixed(2)),
        medianPrice: median
    };
}

const items = [
    { name: "Widget", price: "25.50" },
    { name: "Gadget", price: 100.00 },
    { name: "Cable", price: "5.75" },
    { name: "Adapter", price: 15.00 }
];

console.log(aggregateProductMetrics(items));
