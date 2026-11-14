export const API_BASE = (import.meta.env.VITE_API_URL ?? '').replace(/\/+$/, '');

export class ApiError extends Error {
    /**
     * @param {number} status HTTP-статус (0 — сетевая ошибка)
     * @param {string} url
     * @param {string} body
     */
    constructor(status, url, body) {
        super(`API ${status} for ${url}`);
        this.name = 'ApiError';
        this.status = status;
        this.url = url;
        this.body = body;
    }
}

/**
 * @param {string} path
 * @param {RequestInit} [init]
 * @returns {Promise<Response>}
 */
export async function request(path, init) {
    const url = `${API_BASE}${path.startsWith('/') ? path : `/${path}`}`;
    const headers = new Headers(init?.headers);

    if (!headers.has('Content-Type') && typeof init?.body === 'string') {
        headers.set('Content-Type', 'application/json');
    }

    let response;

    try {
        response = await fetch(url, {...init, headers});
    } catch (cause) {
        throw new ApiError(0, url, cause instanceof Error ? cause.message : String(cause));
    }

    if (!response.ok) {
        throw new ApiError(response.status, url, await response.text());
    }

    return response;
}
