import {describe, expect, it} from 'vitest';
import {createRow, moveRow, removeRow, updateRow} from '@/core/utils/rows';

const ROWS = Object.freeze([
    {id: 'first', topic: 'Первая'},
    {id: 'second', topic: 'Вторая'},
    {id: 'third', topic: 'Третья'},
]);

describe('rows', () => {
    it('создаёт строку с пустыми полями', () => {
        expect(createRow('new', ['topic', 'points'])).toEqual({id: 'new', topic: '', points: ''});
    });

    it('меняет поле только у нужной строки и не трогает исходный массив', () => {
        const nextRows = updateRow(ROWS, 'second', 'topic', 'Новая');

        expect(nextRows[1].topic).toBe('Новая');
        expect(ROWS[1].topic).toBe('Вторая');
    });

    it('удаляет строку по id', () => {
        expect(removeRow(ROWS, 'first').map((row) => row.id)).toEqual(['second', 'third']);
    });

    it('переносит строку на новое место', () => {
        expect(moveRow(ROWS, 0, 2).map((row) => row.id)).toEqual(['second', 'third', 'first']);
    });

    it('не двигает строку за границы списка', () => {
        expect(moveRow(ROWS, 0, -1)).toBe(ROWS);
        expect(moveRow(ROWS, 2, 3)).toBe(ROWS);
    });
});
