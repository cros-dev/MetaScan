import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'formatNumber',
  standalone: true
})
export class FormatNumberPipe implements PipeTransform {
  transform(value: string | number | undefined): string {
    if (value === undefined || value === null || value === '') {
      return '';
    }

    const stringValue = value.toString();

    if (!stringValue.includes('.')) {
      return stringValue;
    }

    return parseFloat(stringValue).toString();
  }
}
