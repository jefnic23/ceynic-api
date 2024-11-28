import type { RequestHandler } from '@sveltejs/kit';
import { BUCKETEER_BUCKET_NAME } from '$env/static/private';

export const GET: RequestHandler = async ({ params }) => {
    const imageUrl = `https://${BUCKETEER_BUCKET_NAME}.s3.amazonaws.com/public/${params.image}`;

    const response = await fetch(imageUrl);

    if (!response.ok) {
        return new Response('Image not found', { status: 404 });
    }

    const blob = await response.blob();
    
    return new Response(blob, {
        headers: {
            'Content-Type': blob.type,
            'Access-Control-Allow-Origin': '*'
        }
    });
};
