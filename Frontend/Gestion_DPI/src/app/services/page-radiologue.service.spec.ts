import { TestBed } from '@angular/core/testing';

import { PageRadiologueService } from './page-radiologue.service';

describe('PageRadiologueService', () => {
  let service: PageRadiologueService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(PageRadiologueService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
