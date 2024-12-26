import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SoinFormComponent } from './soin-form.component';

describe('SoinFormComponent', () => {
  let component: SoinFormComponent;
  let fixture: ComponentFixture<SoinFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SoinFormComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SoinFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
