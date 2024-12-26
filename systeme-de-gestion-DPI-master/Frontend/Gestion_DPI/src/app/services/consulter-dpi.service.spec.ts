import { TestBed } from '@angular/core/testing';

import { ConsulterDpiService } from './consulter-dpi.service';

describe('ConsulterDpiService', () => {
  let service: ConsulterDpiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ConsulterDpiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
