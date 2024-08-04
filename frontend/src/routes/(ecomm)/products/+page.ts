export const load = async ({ fetch, url }) => {
    const fetchProducts = async (sort: string = "") => {
        const queryParams = new URLSearchParams();

        if (sort) {
            queryParams.append("sort", sort);
        }

        const response = await fetch(`http://127.0.0.1:8000/products?${queryParams.toString()}`);

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData = await response.json();

        return responseData;
    }

    const sort = url.searchParams.get("sort") || "";

    return {
        products: fetchProducts(sort)
    }
}