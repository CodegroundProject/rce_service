from marshmallow import Schema, fields
import json


class SchemaSavePlayground(Schema):
    active_lang = fields.Str(required=True)
    lang_buffers = fields.Dict(required=True)
    execution_result = fields.Dict(required=True)


DEFAULT_LANGUAGE = "python"
DEFAULT_LANG_BUFFERS = json.dumps({
    "python": r'''
import numpy as np

def householder(a):
  """
  Computes the Householder transformation of a vector \`a\`.
  Given an m-dimensional vector a, the mxm Householder
  transformation matrix Q is defined as
      Q = I - 2 * v * vT
  where
      v = u / ||u||
      u = x - norm(x) * e_1
  """
  u = a.copy()
  u[0] += np.copysign(np.linalg.norm(a), a[0])
  u_0 = u[0]
  if u_0 == 0:
      u_0 = 1
  v = np.reshape(u / u_0, (-1, 1))

  I = np.eye(a.shape[0])
  vTv = np.dot(v.T, v)
  if vTv == 0:
      vTv = 1
  Q = I - (2 / vTv) * np.dot(v, v.T)
  return Q

def qr_decomposition(A):
  """
  Computes the QR decomposition of a matrix A.
  """
  m, n = A.shape
  R = A.copy()
  Q = np.eye(m)
  for i in range(min(m, n)):
      H = np.eye(m)
      H[i:, i:] = householder(R[i:, i])
      Q = np.dot(Q, H)
      R = np.dot(H, R)
  return Q, R

A = np.array([
 [1, 2, 3],
 [4, 5, 6],
 [7, 8, 9],
 [10, 11, 12],
 [13, 14, 15],
])
Q, R = qr_decomposition(A)

print("Q =", Q)
print("R =", R)
print("A = QR =", np.dot(Q, R))
'''.strip(),

    "javascript": r"""
// Derived from Rado Kirov's blog on incremental computation:
// https://rkirov.github.io/posts/incremental_computation
const {of, Subject} = require('rxjs');
const {map, switchMap, distinctUntilChanged} = require('rxjs/operators');

function doSquare(n) { return n * n; }
function doSqrt(n) { return Math.sqrt(n); }

const sq = new Subject();
const sqrt = new Subject();
const whichOp = new Subject();

const opSq = sq.pipe(map(doSquare), distinctUntilChanged());
const opSqrt = sqrt.pipe(map(doSqrt), distinctUntilChanged());
const op = whichOp.pipe(
    switchMap(which => which === 'sq' ? opSq : opSqrt));

op.subscribe((value) => console.log(`recomputed: ${value}`));

// initial computation for "sq"
op.next('sq');
sq.next(4);
sqrt.next(4);

// re-computation of "opSqrt" with new value
sqrt.next(16);  // no log occurs

// re-computation of "opSq" with new value
sq.next(16);  // log occurs
""".strip(),

    "rust": """
use rand::Rng;
use rand::distributions::{Distribution, Standard};

/// A point in the unit square.
struct PointI2 {
    x: f64,
    y: f64,
}
impl Distribution<PointI2> for Standard {
    fn sample<R: Rng + ?Sized>(&self, rng: &mut R) -> PointI2 {
        PointI2 {
            x: rng.gen_range(0., 1.),
            y: rng.gen_range(0., 1.),
        }
    }
}

fn monte_carlo_pi(sample_size: u64) -> f64 {
    let in_unit_circle = |point: &PointI2| {
        let dx = point.x - 0.5;
        let dy = point.y - 0.5;
        (dx * dx) + (dy * dy) <= 0.25
    };
    let mut rng = rand::thread_rng();

    let num_in_circle = (0..sample_size)
        .map(|_| rng.gen::<PointI2>())
        .filter(in_unit_circle)
        .count() as f64;
    num_in_circle / (sample_size as f64) * 4.
}

fn main() {
    for mag in 3..6 {
        let sample_size = 10_u64.pow(mag);
        let estimate = monte_carlo_pi(sample_size);
        println!("[sample={}]\\t\\tpi ~= {}", sample_size, estimate);
    }
}
""".strip(),

    "cpp": r"""
// Derived from the POCO introduction
// https://pocoproject.org/docs/00100-GuidedTour.html
#include "Poco/BasicEvent.h"
#include "Poco/Delegate.h"
#include <fmt/core.h>
#include <nlohmann/json.hpp>

using Poco::BasicEvent;
using Poco::delegate;
using nlohmann::json;

struct Source {
    BasicEvent<int> theEvent;
    void fireEvent(int n) {
        theEvent(this, n);
    }
};

struct Target {
    void onEvent(const void* pSender, int& arg) {
        json j2 = {{"event", arg}};
        fmt::print("{}\n", j2.dump(4));
    }
};

int main(int argc, char** argv)
{
    Source source;
    Target target;

    // subscribe Target::onEvent to the source
    source.theEvent += delegate(&target, &Target::onEvent);
    source.fireEvent(0);

    // Unsubscribe Target::onEvent to the source
    source.theEvent -= delegate(&target, &Target::onEvent);
    source.fireEvent(1); // no event printed
}
""".strip(),
})
DEFAULT_EXECUTION_RESULT = json.dumps({
    "success": True,
    "exitCode": "",
    "stdout": "",
    "stderr": "",
})
