import type { Product } from '$lib/interfaces/product';

export const load = async ({ fetch }) => {
    const fetchProducts = async (): Promise<Product[]> => {
        const response = await fetch('http://127.0.0.1:8000/products');

        if (!response.ok) {
            console.log("Error retrieving products.");
            return [];
        }

        const responseData = await response.json();

        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        return responseData.map((item: any): Product => ({
            title: item.title,
            price: item.price,
            height: item.height,
            width: item.width, 
            medium: item.mediumId === 1 ? "Painting" : "Print",
            imageUrl: item.imageUrl
        }));
    }

    return {
        products: fetchProducts()
    }
}