import { TestBed } from '@angular/core/testing';


import { CreationDPIService } from './creation-dpi.service';

describe('CreationDPIService', () => {
  let service: CreationDPIService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CreationDPIService);

  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
