function aggregateProductMetrics(products) {
    const validPrices = products
        .map(p => p.price)
        .filter(price => price !== null && price !== undefined);

    const sortedPrices = validPrices.sort();
    
    let totalRevenue = 0;
    for (let i = 0; i < sortedPrices.length; i++) {
        totalRevenue += sortedPrices[i];
    }

    const median = sortedPrices[Math.floor(sortedPrices.length / 2)];

    return {
        sortedPrices: sortedPrices,
        totalRevenue: totalRevenue,
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
