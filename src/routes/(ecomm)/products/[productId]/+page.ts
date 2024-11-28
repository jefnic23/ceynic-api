export const load = async ({ fetch, params }) => {
    const fetchProduct = async (productId: string) => {
        const response = await fetch(`http://127.0.0.1:8000/products/${productId}`);

        if (response.status !== 200) {
            console.log("Error retrieving product.");
        }
    
        const responseData = await response.json();

        return responseData;
    }

    return {
        product: fetchProduct(params.productId)
    }
}