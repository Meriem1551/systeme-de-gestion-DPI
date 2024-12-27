import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BilanBiologiqueComponent } from './bilan-biologique.component';

describe('BilanBiologiqueComponent', () => {
  let component: BilanBiologiqueComponent;
  let fixture: ComponentFixture<BilanBiologiqueComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BilanBiologiqueComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(BilanBiologiqueComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
