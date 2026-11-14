import {describe, expect, it} from 'vitest';
import {getPreviewLines} from '@/core/utils/preview';

describe('preview', () => {
    it('делит текст на абзацы и выбрасывает пустые строки', () => {
        expect(getPreviewLines('Первый\n\n  Второй  ').map((line) => line.text)).toEqual(['Первый', 'Второй']);
    });

    it('превращает строки с дефисом в пункты списка', () => {
        const [paragraph, item] = getPreviewLines('Задачи:\n- изучить SQL');

        expect(paragraph.isListItem).toBe(false);
        expect(item).toMatchObject({text: 'изучить SQL', isListItem: true});
    });
});
